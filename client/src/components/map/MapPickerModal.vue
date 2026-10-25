<!-- client/src/components/map/MapPickerModal.vue -->
<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="modelValue" class="map-modal-overlay" @click.self="$emit('update:modelValue', false)">
        <div class="map-modal-content">
          <div class="map-modal-header">
            <h3>Выберите место на карте</h3>
            <button class="close-btn" @click="$emit('update:modelValue', false)" title="Закрыть">
              <IconFa name="times" />
            </button>
          </div>

          <div class="map-container" ref="mapContainer"></div>

          <div class="map-modal-footer">
            <div class="location-info" v-if="selectedAddress">
              <IconFa name="map-pin" class="me-2" />
              <span>{{ selectedAddress }}</span>
            </div>
            <div class="location-info text-muted" v-else>
              <IconFa name="map-pin" class="me-2" />
              <span>Переместите маркер или кликните на карту для получения адреса</span>
            </div>

            <div class="map-actions">
              <button class="btn btn-secondary" @click="$emit('update:modelValue', false)">Отмена</button>
              <button class="btn btn-primary" @click="confirmSelection" :disabled="!formLatLng">
                <IconFa name="check" class="me-2" /> Подтвердить
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import IconFa from '@/components/ui/IconFa.vue'

const props = defineProps({
  modelValue: Boolean,
  initialLat: Number,
  initialLng: Number
})

const emit = defineEmits(['update:modelValue', 'select'])

const mapContainer = ref(null)
let map = null
let marker = null
const formLatLng = ref(null)
const selectedAddress = ref('')

// Инициализация карты
const initMap = () => {
  if (!mapContainer.value) return

  // По умолчанию центр на Москве, если координаты не переданы
  const startLat = props.initialLat || 55.7558
  const startLng = props.initialLng || 37.6173

  map = L.map(mapContainer.value).setView([startLat, startLng], 14)

  // Слой OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 19
  }).addTo(map)

  // Маркер с возможностью перетаскивания
  marker = L.marker([startLat, startLng], { draggable: true }).addTo(map)
  formLatLng.value = { lat: startLat, lng: startLng }

  fetchAddress(startLat, startLng)

  // Событие перетаскивания маркера
  marker.on('dragend', (event) => {
    const position = marker.getLatLng()
    formLatLng.value = { lat: position.lat, lng: position.lng }
    fetchAddress(position.lat, position.lng)
  })

  // Событие клика по карте
  map.on('click', (event) => {
    marker.setLatLng(event.latlng)
    formLatLng.value = { lat: event.latlng.lat, lng: event.latlng.lng }
    fetchAddress(event.latlng.lat, event.latlng.lng)
  })

  // Исправление бага рендеринга Leaflet в модальных окнах
  setTimeout(() => {
    map.invalidateSize()
  }, 100)
}

// Обратное геокодирование через бесплатный API Nominatim
const fetchAddress = async (lat, lng) => {
  try {
    const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`)
    const data = await response.json()
    if (data && data.display_name) {
      selectedAddress.value = data.display_name
    } else {
      selectedAddress.value = `Координаты: ${lat.toFixed(5)}, ${lng.toFixed(5)}`
    }
  } catch (error) {
    console.error('Geocoding error:', error)
    selectedAddress.value = `Координаты: ${lat.toFixed(5)}, ${lng.toFixed(5)}`
  }
}

const confirmSelection = () => {
  if (formLatLng.value) {
    emit('select', {
      lat: formLatLng.value.lat,
      lng: formLatLng.value.lng,
      address: selectedAddress.value
    })
    emit('update:modelValue', false)
  }
}

// Следим за открытием модального окна
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    setTimeout(() => {
      initMap()
    }, 50)
  } else {
    if (map) {
      map.remove()
      map = null
      marker = null
    }
  }
})

onBeforeUnmount(() => {
  if (map) {
    map.remove()
  }
})
</script>

<style scoped>
.map-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(23, 47, 64, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

.map-modal-content {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 800px;
  height: 600px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.map-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e8edf0;
}

.map-modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 800;
  color: #172f40;
}

.close-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: none;
  background: #f1f5f9;
  color: #70808c;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #e2e8f0;
  color: #172f40;
}

.map-container {
  flex: 1;
  width: 100%;
  z-index: 1;
}

.map-modal-footer {
  padding: 1.25rem 1.5rem;
  border-top: 1px solid #e8edf0;
  background: #f8fafc;
}

.location-info {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #172f40;
  margin-bottom: 1rem;
  line-height: 1.4;
}

.text-muted {
  color: #70808c;
}

.map-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  border: none;
  transition: all 0.2s ease;
}

.btn-secondary {
  background: #f1f5f9;
  color: #172f40;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

.btn-primary {
  background: linear-gradient(135deg, #00a896, #087e8b);
  color: white;
  box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>