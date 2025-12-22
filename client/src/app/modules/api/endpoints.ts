import { environment } from "../environments/environment";

const authenticationRoute = 'authentication';
const applicationRoute = 'application';


export const endpoints = {

  authentication: {
    signIn: `${environment.apiUrl}/${authenticationRoute}/sign-in`,
    signUp: `${environment.apiUrl}/${authenticationRoute}/sign-up`,
    // signOut: `${authenticationRoute}/sign-out`,
    // refreshToken: `${authenticationRoute}/refresh-token`,
  },

}
