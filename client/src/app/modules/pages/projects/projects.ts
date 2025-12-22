import { Component } from '@angular/core';
import { ProjectTreeComponent } from '../../components/trees/project-tree';

@Component({
  standalone: true,
  selector: 'app-projects',
  imports: [ProjectTreeComponent],
  templateUrl: './projects.html',
  styleUrl: './projects.css',
})
export class ProjectsPage {

}
