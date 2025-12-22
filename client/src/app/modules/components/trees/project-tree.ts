import {ChangeDetectionStrategy, Component} from '@angular/core';
import {MatTreeModule} from '@angular/material/tree';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';

/**
 * Food data with nested structure.
 * Each node has a name and an optional list of children.
 */
interface ProjectNode {
  name: string;
  children?: ProjectNode[];
}

@Component({
  standalone: true,
  selector: 'app-project-tree',
  imports: [MatTreeModule, MatButtonModule, MatIconModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './project-tree.html',
  styleUrl: './project-tree.css',
})
export class ProjectTreeComponent {

  dataSource = EXAMPLE_DATA;

  childrenAccessor = (node: ProjectNode) => node.children ?? [];

  hasChild = (_: number, node: ProjectNode) => !!node.children && node.children.length > 0;
}

const EXAMPLE_DATA: ProjectNode[] = [
  {
    name: 'Fruit',
    children: [{name: 'Apple'}, {name: 'Banana'}, {name: 'Fruit loops'}],
  },
  {
    name: 'Vegetables',
    children: [
      {
        name: 'Green',
        children: [{name: 'Broccoli'}, {name: 'Brussels sprouts'}],
      },
      {
        name: 'Orange',
        children: [{name: 'Pumpkins'}, {name: 'Carrots'}],
      },
    ],
  },
];
