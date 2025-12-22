/*
import {
  ChangeDetectionStrategy,
  Component,
  Injector,
  Input,
  OnInit,
  effect,
  inject,
  runInInjectionContext,
} from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { isPlatformBrowser } from '@angular/common';
import { PLATFORM_ID } from '@angular/core';
import { TeamService } from '../../services/team';

@Component({
  selector: 'select-list',
  standalone: true,
  templateUrl: './select-list.component.html',
  styleUrls: ['./select-list.component.css'],
  imports: [MatFormFieldModule, MatSelectModule, ReactiveFormsModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SelectListComponent implements OnInit {
  @Input({ required: true }) control!: FormControl<string>;
  @Input() label = 'Grupo de trabajo';

  private readonly teamService = inject(TeamService);
  private readonly platformId = inject(PLATFORM_ID);
  private readonly injector = inject(Injector);

  // readonly teams = this.teamService.teams;
  // readonly loading = this.teamService.loading;
  // readonly hasError = this.teamService.hasError;

  ngOnInit(): void {
    // Keep the form control disabled in sync with the loading signal
    runInInjectionContext(this.injector, () =>
      effect(() => {
        const shouldDisable = this.loading();
        if (!this.control) return;
        if (shouldDisable && this.control.enabled) {
          this.control.disable({ emitEvent: false });
        } else if (!shouldDisable && this.control.disabled) {
          this.control.enable({ emitEvent: false });
        }
      }),
    );

    if (!isPlatformBrowser(this.platformId)) return;
    if (!this.teams().length && !this.loading()) {
      this.teamService.loadTeams();
    }
  }
}

*/
