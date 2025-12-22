import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSidenavModule } from '@angular/material/sidenav';
import { SidenavComponent } from '../../components/sidenav/sidenav';
import { AuthenticationService } from '../../services/authentication';
import { Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-shell',
  imports: [
    RouterOutlet,
    SidenavComponent,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatSidenavModule,
  ],
  templateUrl: './shell.html',
  styleUrl: './shell.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ShellLayout {
  private readonly authenticationService = inject(AuthenticationService);
  private readonly router = inject(Router);
  protected opened = true;

  protected logout(): void {
    this.authenticationService.signOut();
    this.router.navigate(['/sign-in']);
  }
}
