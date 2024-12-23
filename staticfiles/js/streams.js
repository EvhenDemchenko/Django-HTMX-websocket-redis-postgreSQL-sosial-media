let rtc = {
    localAudioTrack: null,
    localVideoTrack: null,
    client: null,
};

const CHANNEL = sessionStorage.getItem("CHANNEL");
const TOKEN = sessionStorage.getItem("TOKEN");
const UID = sessionStorage.getItem("UID");
const USERNAME = sessionStorage.getItem("USERNAME");



let options = {
    appId: "303468ce452f4351ba2a4a199eb5c1de", 
    channel: CHANNEL,
    token: TOKEN, 
    uid: UID,
};

// Initialize the AgoraRTC client
// Initialize the AgoraRTC client
function initializeClient() {
    rtc.client = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" });
    setupEventListeners();
    
}

// Handle remote user events
function setupEventListeners() {
    rtc.client.on("user-published", async (user, mediaType) => {
        await rtc.client.subscribe(user, mediaType);
        console.log("subscribe success");

        if (mediaType === "video") {
            displayRemoteVideo(user);
        }

        if (mediaType === "audio") {
            user.audioTrack.play();
        }
    });

    rtc.client.on("user-unpublished", (user) => {
        const remotePlayerContainer = document.getElementById(user.uid);
        remotePlayerContainer && remotePlayerContainer.remove();
    });
}

// Display remote video
let  displayRemoteVideo = async (user) => {
    const remoteVideoTrack = user.videoTrack;
    const remotePlayerContainer = document.createElement("div");
    remotePlayerContainer.id = user.uid.toString();
    // remotePlayerContainer.textContent = `Remote user ${user.uid}`;
    remotePlayerContainer.classList.add("video-container");


    document.querySelector("#video-streams").append(remotePlayerContainer);
    let remoteuser = await getMember(user)
    const div = document.createElement("div");
    div.id = user.uid.toString();
    div.textContent = `Remote user ${remoteuser.name}`;
    div.classList.add("username-wrapper");

    remotePlayerContainer.append(div)
    remoteVideoTrack.play(remotePlayerContainer);

}

// Join a channel and publish local media
async function joinChannel() {
    try{
        await rtc.client.join(options.appId, options.channel, options.token, options.uid);
        await createAndPublishLocalTracks();
    }
    catch(e){
        console.log(e);
        window.open('/video/', '_self')
    }
    
    displayLocalVideo();
    console.log("Publish success!");
    
    
}

// Publish local audio and video tracks
async function createAndPublishLocalTracks() {
    rtc.localAudioTrack = await AgoraRTC.createMicrophoneAudioTrack();
    rtc.localVideoTrack = await AgoraRTC.createCameraVideoTrack();
    await rtc.client.publish([rtc.localAudioTrack, rtc.localVideoTrack]);
}

// Display local video
let  displayLocalVideo = async () => {
    const localPlayerContainer = document.createElement("div");
    localPlayerContainer.id = options.uid;

    // localPlayerContainer.textContent = `Local user ${options.uid}`;
    localPlayerContainer.classList.add("video-container");
    document.querySelector("#video-streams").append(localPlayerContainer);
    rtc.localVideoTrack.play(localPlayerContainer);
    const user = await createMember()
    const div = document.createElement("div");
    div.id = options.uid.toString();
    div.textContent = `Remote user ${user.name}`;
    div.classList.add("username-wrapper");

    localPlayerContainer.append(div)

}


// Leave the channel and clean up
async function leaveChannel() {
    // Close local tracks
    rtc.localAudioTrack.close();
    rtc.localVideoTrack.close();

    // Remove local video container
    const localPlayerContainer = document.getElementById(options.uid);
    localPlayerContainer && localPlayerContainer.remove();

    // Remove all remote video containers
    rtc.client.remoteUsers.forEach((user) => {
        const playerContainer = document.getElementById(user.uid);
        playerContainer && playerContainer.remove();
    });
    await deleteMember()
    // Leave the channel
    await rtc.client.leave();
    window.open('/video/', '_self')
}

async function toggleCamera(e) {
    if(rtc.localVideoTrack.muted) {
        await rtc.localVideoTrack.setMuted(false)
        e.target.style.backgroundColor = '#fff'
    }else{
        await rtc.localVideoTrack.setMuted(true)
        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
    }
    
}
async function toggleMicrophone(e) {
    if(rtc.localAudioTrack._volume == 0) {
        await rtc.localAudioTrack.setVolume(100)
        console.log('audio',rtc.localAudioTrack._volume)
        e.target.style.backgroundColor = '#fff'
    }else{
        await rtc.localAudioTrack.setVolume(0)
        console.log('audio',rtc.localAudioTrack._volume)
        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
    }
}



let createMember = async () =>{
    let response = await fetch('/video/create_member/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'name': USERNAME,
            'room_name': CHANNEL,
            'uid': UID

        })
    })

    let member = await response.json()
    return member
}

let getMember = async (user) => {
    console.log('userinfo' , user)
    let response = await fetch(`/video/get_member/?uid=${user.uid}&room_name=${CHANNEL}`)
    let member = await response.json()
    return member
}

let deleteMember = async () => {
    let response = await fetch('/video/delete_member/', {
        method:'POST',
        headers: {
            'Content-Type':'application/json'
        },
        body:JSON.stringify({'name':USERNAME, 'room_name':CHANNEL, 'uid':UID})
    })
    let member = await response.json()
}



// Set up button click handlers
function setupButtonHandlers() {
    document.getElementById("leave-btn").onclick = leaveChannel;
    document.getElementById("camera-btn").onclick = toggleCamera;
    document.getElementById("mice-btn").onclick = toggleMicrophone;
}

// Start the basic call
function startBasicCall() {
    initializeClient();
    joinChannel();
    document.addEventListener("DOMContentLoaded",  setupButtonHandlers);
    window.addEventListener('beforeunload', deleteMember);

}

startBasicCall();