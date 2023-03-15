<script setup>
import Controller from "./Controller.vue";
import Message from "./Message.vue";
import { onUpdated, ref, watchEffect } from "vue";
import { request } from "../services/index.js";

const messageList = ref(null);
const messages = ref([
  { text: "Welcome to the Donald Trump Tweet Generation Bot!", type: "trump" },
  {
    text: "Many are saying I'm the best 140 character writer in the world. Just give me a topic and will tweet the hell out of it!",
    type: "trump",
  },
]);

const processQuestion = async (message, callback) => {
  if (message.length === 0) return;

  //items in list must be chronological
  //messages container error, flavor and normal messages
  messages.value.push({
    text: message,
    type: "user",
  });
  callback();

  //here comes trump or error message
  const response = await request({ user_input: message, fake_tweet: "False" });
  console.log(response);
};

onUpdated(() => {
  messageList.value.scrollTop = messageList.value.scrollHeight;
});
</script>

<template>
  <div class="bg-white w-[55%] h-[70%] bg-opacity-80 flex flex-col">
    <div class="w-full flex flex-col justify-center items-center p-5">
      <p class="font-bold text-3xl text-gray-700">The Trumpbot</p>
    </div>
    <div class="flex-grow overflow-y-auto overflow-x-hidden" ref="messageList">
      <ul>
        <Message
          v-for="message in messages"
          :message="message.text"
          :type="message.type"
        />
      </ul>
    </div>
    <Controller class="w-full" @sendQuestion="processQuestion" />
  </div>
</template>

<style scoped></style>
