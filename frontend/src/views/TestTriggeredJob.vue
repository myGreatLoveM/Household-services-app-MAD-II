<script setup>

async function download() {
  const resp = await fetch('http://localhost:5000/api/export')
  const data = await resp.json() 

  if (!resp.ok) {
    console.log('not ok', data);
    return
  }

  console.log(data);

  const intervalId = setInterval(async () => {
    try {
      const r = await fetch(`http://localhost:5000/api/csv_report/${data.id}`)

      const d = await r.json()

      const status = d.status

      if (status === 'SUCCESS') {
        console.log(d);
        clearInterval(intervalId);  // Stop polling

        //  // Read the response as a Blob
        // const blob = await response.blob();

        // // Create a link element to download the file
        // const fileUrl = window.URL.createObjectURL(blob);
        // const link = document.createElement('a');
        // link.href = fileUrl;
        // link.setAttribute('download', 'sample.pdf');  // Set the filename
        // document.body.appendChild(link);
        // link.click();

        // // Clean up and remove the link element
        // link.remove();



      } else if (status === 'FAILURE') {
        console.error('Task failed');
        clearInterval(intervalId);  // Stop polling
      } 
    } catch (error) {
      console.error("Error checking task status:", error);
      clearInterval(intervalId);  // Stop polling
    }
  }, 1000);  // Poll every 1 second
}


</script>


<template>
  <button @click="download" class="bg-blue-400 text-white px-3 py-1">Download</button>
</template>