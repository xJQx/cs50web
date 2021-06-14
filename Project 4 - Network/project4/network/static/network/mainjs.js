// Edit post function
document.addEventListener("DOMContentLoaded", () => {
    editpost();
    likepost();
})

function editpost()
{
    document.querySelectorAll('button[name="editpost"]').forEach(button => {
        button.onclick = () => {
            post_id = button.value;

            // hide p
            p = document.querySelector(`#p${post_id}`);
            p.style.display = "none";
            
            // show textarea
            textarea = document.querySelector(`#t${post_id}`);
            textarea.style.display = "block";

            // hide edit button and show savebutton
            document.querySelector(`#b${post_id}`).style.display = "none";
            document.querySelector(`#s${post_id}`).style.display = "block";

            // save post function
            savepost(post_id);
        }
    })
}

function savepost(post_id)
{
    // when save button is clicked
    document.querySelector(`#s${post_id}`).onclick = () => {
        content = document.querySelector(`#t${post_id}`).value;
        
        fetch(`/editpost/${post_id}`, {
            method: "PUT",
            body: JSON.stringify({
                content: content
            })
        })

        // make changes to post dynamically
        // show new p
        p = document.querySelector(`#p${post_id}`);
        p.innerHTML = content;
        p.style.display = "block";

        // hide textarea
        textarea = document.querySelector(`#t${post_id}`);
        textarea.style.display = "none";

        // show edit button and hide savebutton
        document.querySelector(`#b${post_id}`).style.display = "block";
        document.querySelector(`#s${post_id}`).style.display = "none";
    }
}

function likepost()
{
    document.querySelectorAll('button[name="likepost"]').forEach(button => {
        button.onclick = () => {
            post_id = button.value;

            fetch(`/likepost/${post_id}`, {
                method: "PUT",
                body: JSON.stringify({
                    likes: 1,
                    type: "like"
                })
            })

            // update post dynamically
            likes = document.querySelector(`button[id='l${post_id}'] span`).innerHTML;
            likes = parseInt(likes) + 1;
            document.querySelector(`button[id='l${post_id}'] span`).innerHTML = likes;

            unlikes = document.querySelector(`button[id='ul${post_id}'] span`).innerHTML;
            unlikes = parseInt(unlikes) + 1;
            document.querySelector(`button[id='ul${post_id}'] span`).innerHTML = unlikes;

            // hide like button and show unlike button
            document.querySelector(`#l${post_id}`).style.display = "none";
            document.querySelector(`#ul${post_id}`).style.display = "block";

            // call unlike function
            unlikepost(post_id);
        }
    })
}

function unlikepost(post_id)
{
    document.querySelectorAll('button[name="unlikepost"]').forEach(button => {
        button.onclick = () => {
            post_id = button.value;

            fetch(`/likepost/${post_id}`, {
                method: "PUT",
                body: JSON.stringify({
                    likes: -1,
                    type: "unlike"
                })
            })

            // update post dynamically
            likes = document.querySelector(`button[id='l${post_id}'] span`).innerHTML;
            likes = parseInt(likes) - 1;
            document.querySelector(`button[id='l${post_id}'] span`).innerHTML = likes;

            unlikes = document.querySelector(`button[id='ul${post_id}'] span`).innerHTML;
            unlikes = parseInt(unlikes) - 1;
            document.querySelector(`button[id='ul${post_id}'] span`).innerHTML = unlikes;

            // hide like button and show unlike button
            document.querySelector(`#l${post_id}`).style.display = "block";
            document.querySelector(`#ul${post_id}`).style.display = "none";
        }
    })
}