import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ResearchResponse {
    task_id: string;
    message: string;
}

export interface StatusResponse {
    status: 'running' | 'completed' | 'failed';
    logs: string[];
    is_running: boolean;
}

export interface ResultResponse {
    result: string | null;
}

@Injectable({
    providedIn: 'root'
})
export class ResearchService {
    private apiUrl = 'http://localhost:8000/api'; // In real app, from environment

    constructor(private http: HttpClient) { }

    startResearch(topic: string): Observable<ResearchResponse> {
        return this.http.post<ResearchResponse>(`${this.apiUrl}/research`, { topic });
    }

    getStatus(taskId: string): Observable<StatusResponse> {
        return this.http.get<StatusResponse>(`${this.apiUrl}/research/${taskId}/status`);
    }

    getResult(taskId: string): Observable<ResultResponse> {
        return this.http.get<ResultResponse>(`${this.apiUrl}/research/${taskId}/result`);
    }
}
