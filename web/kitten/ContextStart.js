//
// Eel functions
//////////////////

python_dialog = bootbox.dialog({
  show:false,
  title:"Please wait",
  message:"<div id='python_message'></div>"
});


eel.expose(python_bootbox);
function python_bootbox(message){
  custom_alert(message);
  //$("#python_message").html(message);
  //python_dialog.modal("show");
}

eel.expose(python_hide_bb);
function python_hide_bb(){
  setTimeout(function(){
    //python_dialog.modal("hide");
  },1000);
}

eel.expose(load_master_json);
function load_master_json(this_json){
  master_json = this_json;
  //renderItems();
  list_surveys();
  first_load = true;
  list_experiments();
  wait_till_exists("list_graphics");
  list_boosts();
  list_trialtypes();
  initiate_actions();
  autoload_boosts();
  wait_till_exists("list_keys");
}

// this is a hack to deal with asynchronous order of parts of the page loading
function wait_till_exists(this_function){
  if(typeof(window[this_function]) == "undefined"){
    setTimeout(function(){
      wait_till_exists(this_function);
    },100);
  } else {
    window[this_function]();
  }
}

switch(dev_obj.context){
  case "gitpod":
  case "server":
  case "github":
    check_authenticated();   //check dropbox
    break;
  case "localhost":
    eel.load_master_json();  //don't use dropbox
    break;
}
