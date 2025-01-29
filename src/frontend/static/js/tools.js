export async function getURL(API_URL) {
    const protocol = window.location.protocol === 'https:' ? 'https:' : 'http:';
    return `${protocol}//${window.location.host}/${API_URL}`;
}