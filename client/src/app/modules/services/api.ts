import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  'providedIn': 'root',
})
export class APIService {
  private http = inject(HttpClient);

  // GET: Solo necesita un genérico para el tipo de respuesta (T)
  get<T>(url: string): Observable<T> {
    return this.http.get<T>(url);
  }

  // PUT: Necesita dos genéricos:
  // T para la Respuesta (lo que devuelve la API)
  // P para la Carga útil (el cuerpo que se envía en 'payload')
  put<T, P>(url: string, payload: P): Observable<T> {
    return this.http.put<T>(url, payload);
  }

  // POST: Igual que PUT, necesita T (Respuesta) y P (Payload)
  post<T, P>(url: string, payload: P): Observable<T> {
    return this.http.post<T>(url, payload);
  }

  // DELETE: Solo necesita un genérico para el tipo de respuesta (T)
  delete<T>(url: string): Observable<T> {
    return this.http.delete<T>(url);
  }
}
