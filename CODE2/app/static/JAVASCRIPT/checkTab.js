// this doesnt work and idk why

const tabs = document.getElementsByClassName("tablinks");

tabs.forEach(tab => 
{
    tab.addEventListener('click', () => 
    {
    // Remove active class from all tabs
    tabs.forEach(t => t.classList.remove('active'));

    // Add active class to the clicked tab
    tab.classList.add("active");
    
    const activeTab = document.getElementsByClassName("active");
    // Store the active tab's ID in localStorage
    localStorage.setItem('activeTab', activeTab.id);
    });
});


window.addEventListener('DOMContentLoaded', () => 
    {
    const activeTabId = localStorage.getItem('activeTab');
    if (activeTabId) 
    {
        const activeTab = document.getElementById(activeTabId);
        if (activeTab) 
        {
            activeTab.classList.add('active');
        }
    }
});