document.addEventListener('DOMContentLoaded', function(e) { 
    like();
    editButtons(e);
    input();
})


function like(){ 

    const like_buttons = document.querySelectorAll('.like_button');
    like_buttons.forEach((btn) => { 
      
        btn.addEventListener("click", function(event) { 
            fetch(`like/${event.target.dataset.id}`, { 
                method: "PUT", 
                mode: "same-origin", 
                headers: { 
                    'X-CSRFToken': csrftoken,
             },
            })
                .then((response) => response.json())
                
                .catch((error) => console.log(error))
                .then( ()=> { 
                    
                    
                    if(btn.classList.contains('far')){ 
                        btn.classList.toggle('fas')
                    } else { 
                        btn.classList.toggle('far')
                    }

                    
                    let get = document.getElementById(`count-${event.target.dataset.id}`);
                    
                    let like = get.innerHTML;

                    if(btn.classList.contains('fas')){ 
                        like++;
                        get.innerHTML = like;
                        
                     }else { 
                        like--;
                        get.innerHTML = like;
                    }

                })
            
        })

    })
        
} 



function editButtons(e) {

        document.querySelectorAll('.edit-button').forEach((btn) => { 
            btn.addEventListener("click", (e) => { 
                
                let id = e.target.id;
                id = id.substring(id.indexOf('-') + 1);
            
                const postContent = document.getElementById(`content-${id}`);
                const postText = postContent.innerHTML;
                const textarea = document.createElement('textarea');
                textarea.setAttribute("class", "modify");
                textarea.value = postText;
                postContent.innerHTML = "";
                postContent.appendChild(textarea);

                document.getElementById(`edit-${id}`).style.display = "none";
                document.getElementById(`save-${id}`).style.display = 'block';
                
                
            })

        })

    }


function save(e) {
   
    
    const text_update = document.querySelector('.modify').value; 
    console.log(text_update)

    let id = e.target.id
    console.log(id)
    
    id = id.substring(id.indexOf('-') + 1);
    console.log(id)

    fetch(`save/${id}`, { 
        method: "PUT", 
        mode: "same-origin", 
        headers: { 
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 
            post_content : text_update,
            post_id : id,

        })
    })
        .then((response) => response.json())
        .catch((error) => console.log(error))
        .then( (data) => { 
            document.querySelector('.modify').style.display = 'none';
            document.getElementById(`content-${id}`).innerHTML = text_update;
            document.getElementById(`edit-${id}`).style.display = 'block';
            document.getElementById(`save-${id}`).style.display = 'none';
            
        })
}

function input() { 
    // submit button disabled
    const submit = document.getElementById('submit');
    submit.disabled = true;

    const type = document.getElementById('type');
    type.onkeyup = () => { 
        if (type.value.length > 0){ 
            submit.disabled = false;
        }else{ 
            submit.disabled = true;
        }
        
    }
}






// document.querySelector('.edit-button').style.display = "none";
// const but = document.createElement('button');
// but.setAttribute("id", `save-${id}`);
// but.style.display = "block";
// but.setAttribute("class", "stylingbtn makeme");
// but.innerHTML = "Save";





