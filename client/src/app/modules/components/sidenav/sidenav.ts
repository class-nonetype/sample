import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';
import { AuthenticationService } from '../../services/authentication';
import { SidenavItem } from '../../interfaces/sidenav';



@Component({
  selector: 'app-sidenav',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive, MatListModule, MatIconModule],
  templateUrl: './sidenav.html',
  styleUrl: './sidenav.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SidenavComponent {
  private readonly router = inject(Router);
  private readonly authenticationService = inject(AuthenticationService);

  readonly navItems: SidenavItem[] = [
    { label: 'Dashboard', icon: 'dashboard', route: '/dashboard' },
    { label: 'Proyectos', icon: 'account_tree', route: '/projects' },
    { label: 'Grupos', icon: 'groups', route: '/null' },
    { label: 'Perfil', icon: 'person', route: '/profile' },
    { label: 'Cerrar sesion', icon: 'logout', action: () => this.handleLogout() },
  ];

  handleClick(item: SidenavItem, event?: MouseEvent): void {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    if (item.action) {
      item.action();
      return;
    }
    if (item.route) {
      this.router.navigateByUrl(item.route);
    }
  }

  private handleLogout(): void {
    this.authenticationService.signOut();
    this.router.navigate(['/sign-in']);
  }
}
