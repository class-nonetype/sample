import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-authentication',
  imports: [ RouterOutlet ],
  templateUrl: './authentication.layout.html',
  styleUrl: './authentication.layout.css',
})
export class AuthenticationLayout {

}
