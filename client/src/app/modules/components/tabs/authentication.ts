import {Component} from '@angular/core';
import {MatTabsModule} from '@angular/material/tabs';
import { SignInFormComponent } from '../forms/sign-in-form';
import { SignUpFormComponent } from '../forms/sign-up-form';




@Component({
  selector: 'tab-group-authentication',
  templateUrl: './authentication.html',
  standalone: true,
  styleUrl: './authentication.css',
  imports: [
    SignInFormComponent,
    SignUpFormComponent,
    MatTabsModule],
})
export class TabGroupAuthenticationComponent {}
