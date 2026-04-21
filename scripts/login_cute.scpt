tell application "Safari"
    activate
    delay 2
    
    -- Tab to account field and type
    tell application "System Events"
        keystroke "141435048"
        delay 0.3
        key code 48 -- Tab
        delay 0.3
        keystroke "29341226Aa"
        delay 0.3
        key code 36 -- Return
    end tell
end tell
