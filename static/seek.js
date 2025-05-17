// Event delegation: listen for clicks on table rows with data-ts to seek video
document.addEventListener("click", function(event) {
    let el = event.target;
    // Traverse up to the <tr> element
    while (el && el.tagName !== "TR") {
        el = el.parentElement;
    }
    if (!el || !el.hasAttribute("data-ts")) {
        return;
    }
    const ts = parseFloat(el.getAttribute("data-ts"));
    // Locate the actual <video> element; Gradio wraps it in a container with id="video_player"
    const wrapper = document.getElementById("video_player");
    let vid = null;
    if (wrapper) {
        // If the wrapper itself is a video element, use it; otherwise query inside
        vid = wrapper.tagName && wrapper.tagName.toLowerCase() === 'video'
            ? wrapper
            : wrapper.querySelector('video');
    }
    // Debug: log the timestamp and the resolved video element
    console.log("SEEK: ts=", ts, "found vid=", vid);
    if (!isNaN(ts) && vid) {
        vid.currentTime = ts;
        vid.play();
    }
});