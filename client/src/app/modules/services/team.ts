/*

import { inject, Injectable, signal } from '@angular/core';
import { APIService } from './api';
import { endpoints } from '../api/endpoints';
import { Team } from '../interfaces/team';

interface TeamsResponse {
  data: Team[];
}

@Injectable({ providedIn: 'root' })
export class TeamService {
  private readonly apiService = inject(APIService);

  readonly teams = signal<Team[]>([]);
  readonly loading = signal<boolean>(false);
  readonly hasError = signal<boolean>(false);

  loadTeams(): void {
    this.loading.set(true);
    this.hasError.set(false);

    this.apiService.get<TeamsResponse>(endpoints.userGroup.list).subscribe({
      next: ({ data }) => {
        const normalized = Array.isArray(data) ? data : [];
        this.teams.set(normalized);
      },
      error: error => {
        console.error('Failed to load teams', error);
        this.hasError.set(true);
        this.loading.set(false);
      },
      complete: () => this.loading.set(false),
    });
  }
}


*/
