export default class UserService {
    public static getAuthHeaders() {
        const headers = new Headers();
        if (!!sessionStorage.accessToken) {
            headers.append(
                'Authorization',
                `Bearer ${sessionStorage.accessToken}`,
            );
        }
        headers.append('Content-Type', 'application/json');
        headers.append(
            'X-CSRFToken',
            document.cookie.replace('csrftoken=', ''),
        );

        return headers;
    }

    public signIn(user: any) {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');

        const req = {
            method: 'POST',
            headers,
            body: JSON.stringify({
                identifier: user.email,
                password: user.password,
            }),
        };
        return fetch(
            `${process.env.VUE_APP_BACKEND_URL}/auth/local`,
            req as any,
        )
            .then((res: Response) => {
                if (res.status >= 400) {
                    return Promise.reject(res.statusText);
                }

                return res.json();
            });
    }

    public signUp(user: any) {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');

        const req = {
            method: 'POST',
            headers,
            body: JSON.stringify({
                username: user.username,
                email: user.email,
                name: user.name,
                password: user.password,
                institution: user.institution,
                city: user.city,
            }),
        };
        return fetch(
            `${process.env.VUE_APP_BACKEND_URL}/auth/local/register`,
            req as any,
        )
            .then((res: Response) => {
                if (res.status >= 400) {
                    return Promise.reject(res.statusText);
                }

                return res.json();
            });
    }

    public forgottenPassword(email: string) {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        return fetch(`${process.env.VUE_APP_BACKEND_URL}/auth/forgot-password`, {
            method: 'POST',
            headers,
            body: JSON.stringify({
                email,
                url: `${process.env.VUE_APP_BACKEND_URL}/admin/plugins/users-permissions/auth/reset-password`,
            }),
        }).then((res: Response) => {
            if (res.status >= 400) {
                return Promise.reject(res.statusText);
            }

            return res.json();
        }).then((response) => {
            alert('Your user received an email');
          })
          .catch((error) => {
            alert('An error occurred: ' + error);
          });
    }
}
