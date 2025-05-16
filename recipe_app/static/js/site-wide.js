async function CookieChecker(){

    const cookies = document.cookie;
    const pattern = /authCookie=\s*(.*?)\s*\|$/;
    const match = cookies.match(pattern);



    if (match) {
        let cookie = match[1];
        let result = await fetch('/checkCookie', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'cookie': cookie})
        });
        const response=result.status;
       if (response ===401){
           document.cookie = "authCookie=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
           window.location.href="/login";
       }

    }
    else {
        window.location.href="/login";
    }

}
const excludedPaths = ["/login","/signup"];
if (!excludedPaths.includes(window.location.pathname)){
    CookieChecker();
}

