export async function getURL(API_URL) {
    const protocol = 'https:';
    return `${protocol}//${window.location.host}${API_URL}`;
}