// admin/src/composables/useExport.js
import * as XLSX from 'xlsx'
import { saveAs } from 'file-saver'
import { useNotifications } from './useNotifications'

export function useExport() {
    const { success, error: showError } = useNotifications()

    /**
     * Экспорт данных в Excel
     * @param {Array} data - массив объектов для экспорта
     * @param {string} filename - имя файла (без расширения)
     * @param {string} sheetName - имя листа
     * @param {Object} columnMap - маппинг полей (опционально)
     */
    function exportToExcel(data, filename = 'export', sheetName = 'Данные', columnMap = null) {
        try {
            if (!data || data.length === 0) {
                showError('Нет данных для экспорта')
                return
            }

            // Если указан columnMap, преобразуем данные
            let exportData = data
            if (columnMap) {
                exportData = data.map(item => {
                    const row = {}
                    Object.entries(columnMap).forEach(([key, label]) => {
                        row[label] = item[key] ?? ''
                    })
                    return row
                })
            }

            // Создаём workbook
            const wb = XLSX.utils.book_new()
            const ws = XLSX.utils.json_to_sheet(exportData)

            // Настраиваем ширину колонок
            const colWidths = Object.keys(exportData[0]).map(key => ({
                wch: Math.max(key.length, 15)
            }))
            ws['!cols'] = colWidths

            XLSX.utils.book_append_sheet(wb, ws, sheetName)

            // Генерируем файл
            const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'array' })
            const blob = new Blob([wbout], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })

            // Добавляем дату к имени файла
            const dateStr = new Date().toISOString().split('T')[0]
            saveAs(blob, `${filename}_${dateStr}.xlsx`)

            success(`Файл "${filename}.xlsx" успешно экспортирован`)
        } catch (err) {
            console.error('Export error:', err)
            showError('Ошибка при экспорте файла')
        }
    }

    return { exportToExcel }
}