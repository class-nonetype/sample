import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  EventEmitter,
  Output,
  inject,
  signal,
} from '@angular/core';
import {
  AbstractControl,
  NonNullableFormBuilder,
  ReactiveFormsModule,
  ValidatorFn,
  Validators,
} from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatStepperModule } from '@angular/material/stepper';
import { HttpErrorResponse } from '@angular/common/http';
import { finalize } from 'rxjs';
import { MatButtonToggleModule } from '@angular/material/button-toggle';

import { AuthenticationService } from '../../services/authentication';
import { SignUpRequestPayload, SignUpResponse } from '../../interfaces/sign-up';

@Component({
  selector: 'sign-up-form',
  standalone: true,
  templateUrl: './sign-up-form.html',
  styleUrls: ['./sign-up-form.css'],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatStepperModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatButtonModule,
    MatButtonToggleModule
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SignUpFormComponent {
  private readonly formBuilder = inject(NonNullableFormBuilder);
  private readonly authenticationService = inject(AuthenticationService);

  readonly loading = signal(false);
  readonly error = signal<string | null>(null);
  readonly success = signal<string | null>(null);

  readonly profileGroup = this.formBuilder.group({
    fullName: this.formBuilder.control('', { validators: [Validators.required, Validators.minLength(3)] }),
    email: this.formBuilder.control('', { validators: [Validators.required, Validators.email] }),
    isActive: this.formBuilder.control(true),
  });

  private readonly passwordsMatchValidator: ValidatorFn = (group: AbstractControl) => {
    const password = group.get('password')?.value as string | undefined;
    const confirmPassword = group.get('confirmPassword')?.value as string | undefined;
    if (!password || !confirmPassword) return null;
    return password === confirmPassword ? null : { passwordMismatch: true };
  };

  readonly accountGroup = this.formBuilder.group(
    {
      username: this.formBuilder.control('', { validators: [Validators.required, Validators.minLength(3)] }),
      password: this.formBuilder.control('', { validators: [Validators.required, Validators.minLength(8)] }),
      confirmPassword: this.formBuilder.control('', { validators: [Validators.required] }),
      showPassword: this.formBuilder.control(false),
    },
    { validators: this.passwordsMatchValidator },
  );

  readonly userGroup = this.formBuilder.group({
    userGroupId: this.formBuilder.control('', { validators: [Validators.required] }),
  });

  readonly profileControls = this.profileGroup.controls;
  readonly accountControls = this.accountGroup.controls;
  readonly userGroupControls = this.userGroup.controls;

  submit(): void {
    if (this.loading()) return;

    this.markAllAsTouched();

    if (this.profileGroup.invalid || this.accountGroup.invalid || this.userGroup.invalid) {
      return;
    }

    this.loading.set(true);
    this.error.set(null);
    this.success.set(null);

    const payload = this.buildPayload();

    this.authenticationService
      .signUp(payload)
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: (response: SignUpResponse) => {
          this.success.set('Cuenta creada correctamente.');
          this.resetForms();
          this.submitEventEmitter.emit(response);
        },
        error: (error: HttpErrorResponse) => {
          //this.error.set(this.resolveErrorMessage(error));

          console.error('Sign-up error:', error);
        },
      });
  }

  private buildPayload(): SignUpRequestPayload {
    const profileValue = this.profileGroup.getRawValue();
    const accountValue = this.accountGroup.getRawValue();
    const userGroupValue = this.userGroup.getRawValue();

    return {
      UserProfile: {
        fullName: profileValue.fullName.trim(),
        email: profileValue.email.trim().toLowerCase(),
        isActive: profileValue.isActive ?? true,
      },
      UserAccount: {
        username: accountValue.username.trim(),
        password: accountValue.password,
      },
      UserGroup: { id: userGroupValue.userGroupId.trim() },
    };
  }

  private markAllAsTouched(): void {
    this.profileGroup.markAllAsTouched();
    this.accountGroup.markAllAsTouched();
    this.userGroup.markAllAsTouched();
  }

  private resetForms(): void {
    this.profileGroup.reset({
      fullName: '',
      email: '',
      isActive: true,
    });
    this.accountGroup.reset({
      username: '',
      password: '',
      confirmPassword: '',
    });
    this.userGroup.reset({
      userGroupId: '',
    });
  }



  @Output() submitEventEmitter = new EventEmitter<SignUpResponse>();
}
