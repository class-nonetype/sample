import {ChangeDetectionStrategy, Component, EventEmitter, inject, Output, signal} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators} from '@angular/forms';
import {FloatLabelType, MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {finalize, map, merge} from 'rxjs';
import { SignInRequest } from '../../interfaces/requests';
import {MatIconModule} from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { AuthenticationService } from '../../services/authentication';
import { SignInResponse } from '../../interfaces/responses';
import { HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { Session } from '../../interfaces/users';
import { toSignal } from '@angular/core/rxjs-interop';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatRadioModule } from '@angular/material/radio';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: "sign-in-form",
  templateUrl: "./sign-in-form.html",
  styleUrls: ["./sign-in-form.css"],
  standalone: true,
  imports: [
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    FormsModule,
    ReactiveFormsModule,
    MatIconModule,

    MatCheckboxModule,
    MatRadioModule,
    MatIconModule,

  ],
  changeDetection: ChangeDetectionStrategy.OnPush,

})
export class SignInFormComponent {

  private readonly authenticationService = inject(AuthenticationService);
  private readonly router = inject(Router);

  readonly formGroup = new FormGroup({
    username: new FormControl<string>('', {
      nonNullable: true,
      validators: [
        Validators.required,
        Validators.minLength(5),
        Validators.maxLength(15),
      ]
    }),

    password: new FormControl<string>('', {
      nonNullable: true,
      validators: [
        Validators.required,
        Validators.minLength(5),
        Validators.maxLength(15),
      ]
    }
  ),
  });
  readonly formControls = this.formGroup.controls;

  readonly loading = signal(false);
  readonly error = signal<string | null>(null);
  readonly showPassword = signal(false);

  hide = signal(true);



  clickEvent(event: MouseEvent) {
    this.hide.set(!this.hide());
    event.stopPropagation();
  }

  submit(): void {
    if ( this.formGroup.invalid || this.loading() ) return;

    this.loading.set(true);
    this.error.set(null);

    const credentials: SignInRequest = this.formGroup.getRawValue();


    console.log('[payload]', credentials);

    this.authenticationService.signIn(credentials)
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: (payload: SignInResponse) => {
          const session = this.authenticationService.establishSession(payload);
          if (!session) {
            this.error.set('Failed to establish session. Please try again.');
            return;
          }

          void this.router.navigate(['/dashboard']);
          this.submitEventEmitter.emit(session);

          console.log('[response]', payload);

        },
        error: (error: HttpErrorResponse) => {
          //this.error.set(this.resolveErrorMessage(error));

          if (error.status === 404) {
            console.log('User not found');
          }

          this.error.set(error.message);
        },
      });

  }


  @Output() submitEventEmitter = new EventEmitter<Session>();
}
