import { Routes } from '@angular/router';
import { ResearchComponent } from './features/research/research.component';

export const routes: Routes = [
    { path: '', component: ResearchComponent },
    { path: '**', redirectTo: '' }
];
