<template>
  <div class="container">
    <div class="button-arrays-container">
      <div class="button-array" v-for="(array, index) in buttonArrays" :key="index">
        <button v-for="(button, btnIndex) in array" :key="btnIndex" class="array-button" @click="navigate(button)">{{
          button }}</button>
      </div>
    </div>
    <div class="center-button-container">
      <button class="center-button">Schliessen</button>
    </div>
  </div>


</template>

<script>
export default {
  name: 'ServerManagement',
  data() {
    return {
      buttonArrays: [
        ['Oasis Settings', 'Freischaltung'],
        ['Abfrage', 'Machines'],
        ['About'],
      ],
    };
  },
  methods: {
    navigate(button) {
      if (button === 'Oasis Settings') {
        console.log('aaaaaaaaaa');
        this.$router.push('/server-management/oasisSetting');
      }
      else if (button == 'Freischaltung') {
        this.$router.push('/server-management/freischaltung');
      }
      else if (button == 'Abfrage') {
        this.$router.push('/server-management/abfrage');
      }
      else if (button == 'About') {
        this.$router.push('/server-management/about');
      }
      // Add more conditions here if you have more buttons that should navigate to different components
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.button-arrays-container {
  margin-top: 100px;
  /* Set top margin to 100px for the entire group of button arrays */
}

.button-array {
  display: flex;
  gap: 10px;
  margin: 30px;
}

.array-button {
  padding: 10px 20px;
  background-color: #007bff;
  border: none;
  color: white;
  cursor: pointer;
  border-radius: 5px;
  width: 300px;
}

.array-button:hover {
  background-color: #0056b3;
}

.center-button-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.center-button {
  padding: 10px 20px;
  background-color: #28a745;
  border: none;
  color: white;
  cursor: pointer;
  border-radius: 5px;
  width: 300px;
  margin-top: 20px;
  /* Adjust if needed */
}

.center-button:hover {
  background-color: #218838;
}
</style>
