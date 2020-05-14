With 2-Factor Authentication (2FA) enabled, the usual git read/write actions cannot be performed with just username/password.

## Instructions
1.  Follow instructions provided in the Personal Access Tokens tutorial.
2.  On the machine of git repo, remove the old `remote` link and add a new one with the below format:
    `git remote add [repo_name] https://oauth2:[token_name]@gitlab.com/user/project_name.git`

## Links
[Personal Access Tokens tutorial](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)
[Authentication](https://forum.gitlab.com/t/authenticate-using-access-token/9330)