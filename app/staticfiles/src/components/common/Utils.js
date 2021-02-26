// @flow
import jwtDecode from 'jwt-decode';
import { Cookies } from 'react-cookie';

/**
 * Checks if user is authenticated
 */
const isUserAuthenticated = () => {
    const user = getLoggedInUser();
    if (!user) {
        return false;
    }
    const decoded = jwtDecode(user.token);
    const currentTime = Date.now() / 1000;
    if (decoded.exp < currentTime) {
        console.warn('access token expired');
        return false;
    } else {
        return true;
    }
};

/**
 * Returns the logged in user
 */
const getLoggedInUser = () => {
    const user = localStorage.getItem('userInfo') ? localStorage.getItem('userInfo') : null;
    return user ? JSON.parse(user) : null;
};

export { isUserAuthenticated, getLoggedInUser };
