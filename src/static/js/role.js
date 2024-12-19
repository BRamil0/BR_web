export async function getRolesForUser(user) {
    try {
        const response = await fetch(`/api/roles/get_roles_for_user/${user}`);
        if (!response.ok) {
            console.error(`Failed to load language file for "role_list"`);
            return false;
        }
        return await response.json();
    }
    catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        return false;
    }
}

export async function getRole(user, role_name) {
    try {
        const response = await fetch(`/api/roles/get_roles_for_user/${user}`);
        if (!response.ok) {
            console.error(`Failed to load language file for "role_list"`);
            return false;
        }
        const data = await response.json();
        console.log(data);
        for (let role of data) {
            if (role['default_name'] === role_name) {
                return role;
            }
        }
        return false;
    }
    catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        return false;
    }
}

export async function isPermission(roles, permission) {
    try {
        for (const role of roles) {
            if (await checkPermission(role, permission)) {
                return true;
            }
        }
    } catch (error) {
        console.error(`Check permission error: ${error}`);
    }
    return false;
}

async function checkPermission(obj, permission) {
    for (const field in obj) {
        if (field !== 'date_added' && field !== 'end_date') {
            if (obj[field] === permission) {
                return true;
            } else if (typeof obj[field] === 'object' && obj[field] !== null) {
                if (await checkPermission(obj[field], permission)) {
                    return true;
                }
            }
        }
    }
    return false;
}