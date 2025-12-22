import { Injectable, computed, inject, signal } from '@angular/core';

import { SignInRequest } from '../interfaces/requests';
import { SignInResponse } from '../interfaces/responses';
import { SignUpRequestPayload, SignUpResponse } from '../interfaces/sign-up';
import { Session } from '../interfaces/users';

import { endpoints } from '../api/endpoints';
import { APIService } from './api';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';

import { v4 as uuidv4 } from 'uuid';



@Injectable({ providedIn: 'root' })
export class AuthenticationService {

  private router = inject(Router);
  private readonly apiService = inject(APIService);

  private readonly sessionSignal = signal<Session | null>(null);
  readonly accessToken = computed(() => this.sessionSignal()?.accessToken ?? null);
  private readonly storageKey = '__auth_session__';

  readonly currentUserFullName = computed(() => this.sessionSignal()?.userFullName ?? 'Invitado');

  constructor() {
    this.hydrateFromStorage();
  }


  isValidSession(): boolean {
    return !!this.accessToken();
  }

  signIn(payload: SignInRequest): Observable<SignInResponse> {
    return this.apiService.post<SignInResponse, SignInRequest>(endpoints.authentication.signIn, payload);
  }

  signUp(payload: SignUpRequestPayload): Observable<SignUpResponse> {
    return this.apiService.post<SignUpResponse, SignUpRequestPayload>(endpoints.authentication.signUp, payload);
  }


  clearSession() {
    this.sessionSignal.set(null);
    this.persistSession(null);
  }

  signOut() {
    this.clearSession();
    this.router.navigate(['/sign-in']);
  }


  establishSession(session: Session) {
    const normalized = this.normalizeSession(session);
    this.sessionSignal.set(normalized);
    this.persistSession(normalized);
    return normalized;
  }

  private normalizeSession(session: Session | null): Session | null {
    if (!session?.accessToken) return null;
    return {
      accessToken: session.accessToken,
      user: session.user,
      userFullName: session.userFullName,
      userGroupName: session.userGroupName,
    };
  }

  private hydrateFromStorage(): void {
    const persisted = this.readPersistedSession();
    if (persisted) {
      this.sessionSignal.set(persisted);
    }
  }

  private persistSession(session: Session | null): void {
    try {
      if (!session) {
        localStorage.removeItem(this.storageKey);
        return;
      }
      localStorage.setItem(this.storageKey, JSON.stringify(session));
    } catch {
      // Si el storage falla, seguimos solo con la sesión en memoria.
    }
  }

  private readPersistedSession(): Session | null {
    try {
      const raw = localStorage.getItem(this.storageKey);
      return raw ? this.normalizeSession(JSON.parse(raw) as Session) : null;
    } catch {
      return null;
    }
  }
}
