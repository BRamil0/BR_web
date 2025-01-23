export async function sendingDataToInformant() {
    const data = {
        innerWidth: window.innerWidth.toString(),
        innerHeight: window.innerHeight.toString(),
        screen_width: screen.width.toString(),
        screen_height: screen.height.toString(),
        userAgent: navigator.userAgent,
        platform: navigator.platform,
        language: navigator.language,
        location_href: window.location.href,
        connection_downlink: navigator.connection ? navigator.connection.downlink.toString() : 'unknown',
        connection_effective_type: navigator.connection ? navigator.connection.effectiveType : 'unknown',
        online: navigator.onLine.toString(),
        performance_timing: JSON.stringify(performance.timing),

        max_touch_points: navigator.maxTouchPoints.toString(),
        hardware_concurrency: navigator.hardwareConcurrency.toString(),
        device_memory: navigator.deviceMemory ? navigator.deviceMemory.toString() : 'unknown',
        color_depth: screen.colorDepth.toString(),
        pixel_depth: screen.pixelDepth.toString(),
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        cookies_enabled: navigator.cookieEnabled.toString(),
        referrer: document.referrer || 'no-referrer',
        visibility_state: document.visibilityState,
        document_title: document.title,
        page_load_time: (performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart).toString()
    };

    try {
        const response = await fetch('/api/telegram/info/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        return await response.json();
    } catch (error) {
        console.error('Error sending browser info:', error);
        return false;
    }
}