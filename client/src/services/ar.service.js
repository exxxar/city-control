// client/src/services/ar.service.js
import * as THREE from 'three'

class ArService {
  constructor() {
    this.scene = null
    this.camera = null
    this.renderer = null
    this.markers = []
    this.isRunning = false
    this.animationFrameId = null
  }

  init(containerElement) {
    if (!containerElement) return

    // Сцена
    this.scene = new THREE.Scene()

    // Камера
    this.camera = new THREE.PerspectiveCamera(
      75,
      containerElement.clientWidth / containerElement.clientHeight,
      0.1,
      1000
    )
    this.camera.position.set(0, 1.6, 0) // Высота глаз пользователя

    // Рендерер
    this.renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true })
    this.renderer.setSize(containerElement.clientWidth, containerElement.clientHeight)
    this.renderer.setPixelRatio(window.devicePixelRatio)
    containerElement.appendChild(this.renderer.domElement)

    // Освещение
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8)
    this.scene.add(ambientLight)

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5)
    directionalLight.position.set(0, 10, 5)
    this.scene.add(directionalLight)

    // Обработка изменения размера окна
    window.addEventListener('resize', () => this.handleResize(containerElement))
  }

  handleResize(containerElement) {
    if (!this.camera || !this.renderer) return
    this.camera.aspect = containerElement.clientWidth / containerElement.clientHeight
    this.camera.updateProjectionMatrix()
    this.renderer.setSize(containerElement.clientWidth, containerElement.clientHeight)
  }

  createFlag(color = 0xff0000, height = 1.5) {
    // Простой флажок: шест + треугольник
    const group = new THREE.Group()

    // Шест
    const poleGeometry = new THREE.CylinderGeometry(0.02, 0.02, height, 8)
    const poleMaterial = new THREE.MeshBasicMaterial({ color: 0x333333 })
    const pole = new THREE.Mesh(poleGeometry, poleMaterial)
    pole.position.y = height / 2
    group.add(pole)

    // Флажок (треугольник)
    const flagShape = new THREE.Shape()
    flagShape.moveTo(0, 0)
    flagShape.lineTo(0.4, 0.15)
    flagShape.lineTo(0, 0.3)

    const flagGeometry = new THREE.ShapeGeometry(flagShape)
    const flagMaterial = new THREE.MeshBasicMaterial({
      color,
      side: THREE.DoubleSide
    })
    const flag = new THREE.Mesh(flagGeometry, flagMaterial)
    flag.position.y = height - 0.3
    group.add(flag)

    return group
  }

  addProblemMarker(problem, position) {
    let color = 0xffffff // Белый - потенциальная
    if (problem.status === 'new' || problem.priority_id === 1) color = 0xff0000 // Красный - критическая
    else if (['in_progress', 'confirmed'].includes(problem.status)) color = 0xffff00 // Жёлтый - в работе
    else if (['resolved', 'closed'].includes(problem.status)) color = 0x00ff00 // Зелёный - решена

    const flag = this.createFlag(color)
    flag.position.set(position.x, position.y, position.z)
    flag.userData = { problemId: problem.id, problem }

    this.scene.add(flag)
    this.markers.push(flag)

    return flag
  }

  removeMarker(marker) {
    this.scene.remove(marker)
    this.markers = this.markers.filter(m => m !== marker)
  }

  clearMarkers() {
    this.markers.forEach(marker => this.scene.remove(marker))
    this.markers = []
  }

  start() {
    if (this.isRunning) return
    this.isRunning = true
    this.animate()
  }

  animate() {
    if (!this.isRunning) return

    this.animationFrameId = requestAnimationFrame(() => this.animate())

    // Флажки всегда смотрят на камеру (billboard effect)
    this.markers.forEach(marker => {
      marker.lookAt(this.camera.position)
    })

    this.renderer.render(this.scene, this.camera)
  }

  stop() {
    this.isRunning = false
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId)
    }
  }

  destroy() {
    this.stop()
    this.clearMarkers()

    if (this.renderer) {
      this.renderer.dispose()
      this.renderer.domElement.remove()
    }

    this.scene = null
    this.camera = null
    this.renderer = null
  }

  // Raycasting для клика по флажкам
  onClick(event, containerElement) {
    if (!this.camera || !this.renderer) return null

    const rect = containerElement.getBoundingClientRect()
    const x = ((event.clientX - rect.left) / rect.width) * 2 - 1
    const y = -((event.clientY - rect.top) / rect.height) * 2 + 1

    const raycaster = new THREE.Raycaster()
    raycaster.setFromCamera(new THREE.Vector2(x, y), this.camera)

    const intersects = raycaster.intersectObjects(this.markers, true)

    if (intersects.length > 0) {
      // Ищем родительский объект с userData
      let obj = intersects[0].object
      while (obj && !obj.userData.problemId) {
        obj = obj.parent
      }
      return obj ? obj.userData.problem : null
    }

    return null
  }
}

export const arService = new ArService()