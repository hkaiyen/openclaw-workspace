tell application "Reminders"
    set remLists to every reminder list
    set output to "=== Reminders ===" & return
    
    repeat with remList in remLists
        set listName to name of remList
        set output to output & "[" & listName & "]" & return
        
        set rems to every reminder in remList whose completed is false
        repeat with rem in rems
            set remName to name of rem
            if remName is not "" then
                set output to output & "[ ] " & remName & return
            end if
        end repeat
    end repeat
end tell

return output
