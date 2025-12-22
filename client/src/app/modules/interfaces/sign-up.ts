export interface SignUpProfilePayload {
  fullName: string;
  email: string;
  isActive: boolean;
}

export interface SignUpAccountPayload {
  username: string;
  password: string;
}

export interface SignUpGroupPayload {
  id: string;
}

export interface SignUpRequestPayload {
  UserProfile: SignUpProfilePayload;
  UserAccount: SignUpAccountPayload;
  UserGroup: SignUpGroupPayload;
}

export interface SignUpResponse {
  status: boolean;
  message: string;
}
