var App = (function () {
  'use strict';
  
  App.uiNotifications = function( ){  
    
    $('#not-success').click(function(){
      $.gritter.add({
        title: 'Success',
        text: 'This is a simple Gritter Notification.',
        class_name: 'color success'
      });
    });
    

    /*Alt Colors*/
    
    $('#not-dark').click(function(){
      $.gritter.add({
        title: 'Dark Color',
        text: 'This is a simple Gritter Notification.',
        class_name: 'color dark'
      });
    });

  };

  return App;
})(App || {});
