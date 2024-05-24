document.addEventListener('DOMContentLoaded', () => {
    const signUpButton = document.getElementById('sign-up');
    const loginButton = document.getElementById('login');
    const togglePasswordButton = document.getElementById('toggle-password');
    const passwordInput = document.getElementById('password');

    // Adjust button styles based on the current page
    if (window.location.pathname.includes('login')) {
        if (loginButton) {
            loginButton.classList.add('active');
        }
    } else if (window.location.pathname.includes('signUp')) {
        if (signUpButton) {
            signUpButton.classList.add('active');
        }
    }

    // Navigation handling
    if (signUpButton) {
        signUpButton.addEventListener('click', () => {
            window.location.href = '../templates/signUp.html';
        });
    }

    if (loginButton && window.location.pathname.includes('signUp')) {
        loginButton.addEventListener('click', () => {
            window.location.href = '../templates/login.html';
        });
    }

    // Password toggle handling
    if (togglePasswordButton && passwordInput) {
        togglePasswordButton.addEventListener('click', () => {
            if (passwordInput.value.length > 0) {
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    togglePasswordButton.className = 'fas fa-eye-slash';
                } else {
                    passwordInput.type = 'password';
                    togglePasswordButton.className = 'fas fa-eye';
                }
            } else {
                alert("Please enter a password.");
            }
        });
    }

    // const forgotPasswordLink = document.getElementById('forgot-password');
    // if (forgotPasswordLink) {
    //     forgotPasswordLink.addEventListener('click', () => {
    //         alert('Forgot password functionality will be implemented later.');
    //     });
    // }
});

