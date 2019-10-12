<template>
    <b-container fluid class="main-container">
        <b-row>
            <h2>Picture Style Chooser</h2>
            <hr>
        </b-row>
        <b-row>
            <b-card-group deck>
                <b-card title="Title" img-src="https://dummyimage.com/360x640/000/fff&text=Style1" img-alt="Image" img-top>
                  <b-card-text>
                    This is a wider card with supporting text below as a natural lead-in to additional content.
                    This content is a little bit longer.
                  </b-card-text>
                </b-card>

               <b-card title="Title" img-src="https://dummyimage.com/360x640/000/fff&text=Style2" img-alt="Image" img-top>
                  <b-card-text>
                    This is a wider card with supporting text below as a natural lead-in to additional content.
                    This content is a little bit longer.
                  </b-card-text>
                </b-card>

               <b-card  title="Title" img-src="https://dummyimage.com/360x640/000/fff&text=Style3" img-alt="Image" img-top>
                  <b-card-text>
                    This is a wider card with supporting text below as a natural lead-in to additional content.
                    This content is a little bit longer.
                  </b-card-text>
                </b-card>
                 <b-card  title="Title" img-src="https://dummyimage.com/360x640/000/fff&text=Style3" img-alt="Image" img-top>
                  <b-card-text>
                    This is a wider card with supporting text below as a natural lead-in to additional content.
                    This content is a little bit longer.
                  </b-card-text>
                </b-card>
                 <b-card  title="Title" img-src="https://dummyimage.com/360x640/000/fff&text=Style3" img-alt="Image" img-top>
                  <b-card-text>
                    This is a wider card with supporting text below as a natural lead-in to additional content.
                    This content is a little bit longer.
                  </b-card-text>
                </b-card>
              </b-card-group>
        </b-row>
        <b-row>
            <h2>Payment / Coin Status</h2>
            <hr>
        </b-row>
        <b-row>
            Info on Sum<br/>
            Second Line<br/>
            Third line<br/>
            <b-button>Reset button</b-button>
        </b-row>
        <b-row>
            <h2>Camera Status</h2>
            <hr>
        </b-row>
        <b-row>
            Info on Camera<br/>
            Second Line<br/>
            Third line<br/>
        </b-row>
        <b-row>
            <h2>Printer Status</h2>
            <hr>
        </b-row>
        <b-row>
            <b-col>
                Info on Printer 1 of 2<br/>
                Second Line<br/>
                Third line<br/>
            </b-col>
            <b-col>
                Info on Printer 2 of 2<br/>
                Second Line<br/>
                Third line<br/>
            </b-col>
        </b-row>
        <b-row>
            <h2>Log</h2>
            <hr>
        </b-row>
        <b-row>
            <b-form-textarea
              id="textarea-rows"
              placeholder="Log textarea"
              rows="8"
              disabled
            ></b-form-textarea>
        </b-row>
        <b-row>
            <h2>Actions</h2>
            <hr>
        </b-row>
        <b-row>
            <b-button size="lg" class="mx-auto w-20 mh-10 b-critical">PUSH TO TALK</b-button>
            <b-button size="lg" class="mx-auto w-20 mh-10 b-critical">TAKE PICTURE</b-button>
            <b-button size="lg" class="mx-auto w-20 mh-10 b-critical">PRINT CURRENT</b-button>
            <!--- lowermost row --->
        </b-row>
    </b-container>
</template>

<script>
  import io from 'socket.io-client';

  export default {
    components: { 
       
    },
    created: function () {
      window.addEventListener('keyup', this.onkey)
    },
    data: () => ({
      socket: io(require("os").hostname()+':3001')    
    }),
    methods: {
      sendMessage(msg) {
        this.socket.emit('SEND_MESSAGE', {
          user: "mee",
          message: msg,
        });
      },
      onkey(event){
        this.socket.emit('KEYB_INPUT', 10);
        console.log("Keydown "+event);
      },
      formatPrice(value) {
        let val = (value/1).toFixed(2).replace('.', ',')
        return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")
      },      
    },
    mounted() {
      this.socket.on('CLIENT_LIST', (data) => {
          console.log(data);          
      });
      this.socket.emit('REGISTER_CLIENT', 'uicontrol');
    }
  }
</script>

<style>
    .w-20 {
        width:20vw;
    }
    .h-20 {
        height: 3vh;
    }
    .mh-10 {
        min-height: 10vh;
    }
    .b-critical {
        background-color: #ee6600;
        font-size: 2em;
    }
</style>