const temp = document.querySelector('#temperature');
const hum = document.querySelector('#humidity');

const toggle = document.querySelector('#toggle');
let state = 0;

const baseUrl = `http://${host}`;

const toggleSwitch = () => {
  if (!state) {
    toggle.classList.add('active');
  }

  if (state) {
    toggle.classList.remove('active');
  }

  state = !state;
  toggle.innerHTML = !state ? 'OFF' : 'ON';
};

toggle.addEventListener('click', async () => {
  toggleSwitch();

  await fetch(`${baseUrl}/api/switch`, { method: 'POST' });
});

setTimeout(async () => {
  const response = await fetch(`${baseUrl}/api/all-devices`);
  const data = await response.json();

  temp.innerHTML = data.temperature;
  hum.innerHTML = data.humidity;

  state = !data.switch;
  toggleSwitch();
}, 0);

setInterval(async () => {
  const response = await fetch(`${baseUrl}/api/hd11`);
  const data = await response.json();

  temp.innerHTML = data.temperature;
  hum.innerHTML = data.humidity;
}, 5_000);
