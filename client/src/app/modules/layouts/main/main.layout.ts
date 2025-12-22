import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';


@Component({
  standalone: true,
  selector: 'app-main',
  imports: [ RouterOutlet ],
  templateUrl: './main.layout.html',
  styleUrl: './main.layout.css',
})
export class MainLayout {

}
