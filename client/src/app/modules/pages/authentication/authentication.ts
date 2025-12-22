import { Component, inject, OnInit } from '@angular/core';
import { TabGroupAuthenticationComponent } from '../../components/tabs/authentication';

import { AuthenticationService } from '../../services/authentication';
import { Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-sign-in',
  imports: [
    TabGroupAuthenticationComponent
  ],
  templateUrl: './authentication.html',
  styleUrl: './authentication.css',
})
export class AuthenticationPage implements OnInit {

  private router = inject(Router);
  private authenticationService = inject(AuthenticationService);


  ngOnInit() {
    if ( this.authenticationService.isValidSession() ) {
      this.router.navigate(['/dashboard']);
    }
  }

}
