<template>
  <div>
    <b-row>
      <b-col cols="6">
        <b-button
          size="lg"
          :variant="checkingIn ? 'danger' : 'primary'"
          @click="onClick"
        >
          {{ checkingIn ? 'Stop' : 'Start'}} Check In
        </b-button>
        <b-img
          v-if="checkingIn && qrcodeURL"
          center
          style="margin-top: 10px"
          height="500px"
          :src="qrcodeURL"
          alt="Center image"
        ></b-img>
      </b-col>
      <b-col cols="6">
        <textarea id="chat-log" cols="50" rows="20"></textarea><br/>
        <input id="chat-message-input" type="text" size="50"/><br/>
        <input id="chat-message-submit" type="button" value="Send"/>
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  data () {
    return {
      isLoading: false,
      checkingIn: false,
      checkinToken: null,
      qrcodeURL: null,
      location: window.location,
      chatSocket: null
    }
  },
  mounted () {
    this.refresh()

    console.log('ready to connect')
    this.chatSocket = new WebSocket(
        'ws://' + 'localhost:8000' +
        '/ws/chat/lobby/');

    this.chatSocket.onmessage = (e) => {
        var data = JSON.parse(e.data);
        var message = data['message'];
        document.querySelector('#chat-log').value += (message + '\n');
    };

    this.chatSocket.onclose = (e) => {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = (e) => {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = (e) => {
        var messageInputDom = document.querySelector('#chat-message-input');
        var message = messageInputDom.value;
        this.chatSocket.send(JSON.stringify({
            'message': message
        }));

        messageInputDom.value = '';
    };
  },
  destroyed () {
    this.chatSocket.close()
  },
  methods: {
    onClick () {
      if (this.checkingIn) {
        this.isLoading = true
        this.axios.delete(`api/checkin/${this.checkinToken}/stop/`)
          .then(res => {
            this.isLoading = false
            console.log(res)
            if (res.status < 300) {
              this.checkingIn = false
            } else {
              alert('failed to stop check in')
            }
          })
          .catch(err => {
            alert('failed to stop check in')
            console.log(err)
          })
      } else {
        this.isLoading = true
        this.axios.post('api/checkin/start/', {
          event_id: this.$route.params.id
        })
          .then(res => {
            this.isLoading = false
            console.log(res.data)
            if (res.status === 201) {
              this.checkingIn = true
              this.checkinToken = res.data.checkin_token
              this.getQrcode()
            } else {
              alert('failed to start check in')
            }
          })
          .catch(err => {
            alert('failed to start check in')
            console.log(err)
          })
      }
    },
    refresh () {
      this.isLoading = true
      this.axios.get(`api/event/${this.$route.params.id}/checkin/`)
        .then(res => {
          this.isLoading = false
          console.log(res.data)
          if (res.status === 200) {
            this.checkingIn = true
            this.checkinToken = res.data.checkin_token
            this.getQrcode()
          }
        })
        .catch(err => {
          this.isLoading = false
          console.log('failed to fetch events\n', err)
        })
    },
    getQrcode () {
      console.log(`http://${this.location.host}/#/checkin/${this.checkinToken}`)
      this.axios.post('/api/qrcode/', {
        text: `http://${this.location.host}/#/checkin/${this.checkinToken}`
      }, {
        responseType: 'blob'
      })
        .then(res => {
          console.log(res)
          const qrcode = new Blob([res.data], { type: 'image/png' })
          this.qrcodeURL = URL.createObjectURL(qrcode)
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>
