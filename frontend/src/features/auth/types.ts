export type RegisterUserRequest = {
  email: string;
  password: string;
};

export type RegisteredUser = {
  id: string;
  email: string;
  created_at: string;
};

export type AccessTokenResponse = {
  access_token: string;
  token_type: "bearer";
};

export type CurrentUser = {
  id: string;
  email: string;
  created_at: string;
};
