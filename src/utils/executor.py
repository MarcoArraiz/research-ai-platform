import concurrent.futures
import threading
import queue
from typing import Optional, Any

class ResearchExecutor:
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.future: Optional[concurrent.futures.Future] = None
        self.logs = queue.Queue()
        self.result = None
        self.is_running = False

    def submit(self, fn, *args, **kwargs):
        if self.is_running:
            return False
        
        self.is_running = True
        self.result = None
        # Clear queue
        with self.logs.mutex:
            self.logs.queue.clear()
            
        self.future = self.executor.submit(self._run_wrapper, fn, *args, **kwargs)
        return True

    def _run_wrapper(self, fn, *args, **kwargs):
        try:
            result = fn(*args, **kwargs)
            self.result = result
            return result
        except Exception as e:
            self.logs.put(f"ERROR: {str(e)}")
            raise e
        finally:
            self.is_running = False

    def get_logs(self):
        logs = []
        while not self.logs.empty():
            try:
                logs.append(self.logs.get_nowait())
            except queue.Empty:
                break
        return logs

    def check_status(self):
        if self.future and self.future.done():
            self.is_running = False
            try:
                return self.future.result()
            except Exception as e:
                return f"Error: {str(e)}"
        return None
