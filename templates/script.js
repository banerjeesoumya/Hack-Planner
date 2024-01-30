/**Function to set reminder to the user of their added task */

function setReminder(item)
{
    setTimeout(function() 
    {
        var reminder = confirm ("Reminder: " + item);
    }, 5 * 1000); //5 seconds in milliseconds
}