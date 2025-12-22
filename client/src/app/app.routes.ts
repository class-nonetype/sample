// src/app/app.routes.ts
import { Routes } from '@angular/router';
import { AuthenticationLayout } from './modules/layouts/authentication/authentication.layout';
import { authenticationGuard } from './modules/guards/authentication.guard';
import { AuthenticationPage } from './modules/pages/authentication/authentication';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'dashboard' },

  {
    path: '',
    component: AuthenticationLayout,
    children: [
      { path: 'sign-in', component: AuthenticationPage },
    ],
  },

  // 3. Rutas PRIVADAS (Protegidas por Guard)
  {
    path: '',
    canActivate: [authenticationGuard],
    // canActivateChild ya cubre a los hijos, no hace falta ponerlo en cada uno
    canActivateChild: [authenticationGuard],
    loadComponent: () => import('./modules/layouts/shell/shell').then(m => m.ShellLayout),
    children: [
      {
        path: 'dashboard',
        loadComponent: () => import('./modules/pages/dashboard/dashboard').then(m => m.DashboardPage),
      },
      {
        path: 'profile',
        loadComponent: () => import('./modules/pages/profile/profile').then(m => m.ProfilePage),
      },
      {
        path: 'projects',
        loadComponent: () => import('./modules/pages/projects/projects').then(m => m.ProjectsPage),
      },
    ],
  },

  // 4. Comodín (Wildcard) - Enviar a un 404 o al dashboard (que el guard redirigirá)
  { path: '**', redirectTo: 'dashboard' },
];
