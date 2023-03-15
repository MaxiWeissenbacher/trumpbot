<script setup>
import ChatBox from "./components/ChatBox.vue";
import Footer from "./components/Footer.vue";
import InfoBox from "./components/InfoBox.vue";
</script>

<template>
  <main
    class="w-screen h-screen m-auto overflow-hidden bg-[url(assets/bg_whitehouse.jpeg)] bg-cover bg-no-repeat bg-fixed bg-center flex flex-col justify-center items-center"
  >
    <ChatBox />
    <InfoBox />
    <Footer />
  </main>
</template>

<style scoped></style>
