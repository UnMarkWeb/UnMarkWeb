
document.addEventListener('DOMContentLoaded', () => {
    const modeAddBtn = document.getElementById('mode-add-btn');
    const modeRemoveBtn = document.getElementById('mode-remove-btn');
    const toolsAdd = document.getElementById('tools-add');
    const toolsRemove = document.getElementById('tools-remove');
    const processBtnText = document.getElementById('process-btn-text');
    const processBtnIcon = document.getElementById('process-btn-icon');

    modeAddBtn.addEventListener('click', () => {
        modeAddBtn.classList.replace('text-on-surface-variant', 'text-primary');
        modeAddBtn.classList.replace('hover:bg-surface-variant', 'bg-surface-container-lowest');
        modeAddBtn.classList.add('shadow-sm');

        modeRemoveBtn.classList.replace('text-primary', 'text-on-surface-variant');
        modeRemoveBtn.classList.replace('bg-surface-container-lowest', 'hover:bg-surface-variant');
        modeRemoveBtn.classList.remove('shadow-sm');

        toolsAdd.classList.remove('hidden');
        toolsRemove.classList.add('hidden');

        processBtnText.textContent = 'Añadir Marcas de Agua';
        processBtnIcon.textContent = 'add_photo_alternate';
    });

    modeRemoveBtn.addEventListener('click', () => {
        modeRemoveBtn.classList.replace('text-on-surface-variant', 'text-primary');
        modeRemoveBtn.classList.replace('hover:bg-surface-variant', 'bg-surface-container-lowest');
        modeRemoveBtn.classList.add('shadow-sm');

        modeAddBtn.classList.replace('text-primary', 'text-on-surface-variant');
        modeAddBtn.classList.replace('bg-surface-container-lowest', 'hover:bg-surface-variant');
        modeAddBtn.classList.remove('shadow-sm');

        toolsRemove.classList.remove('hidden');
        toolsAdd.classList.add('hidden');

        processBtnText.textContent = 'Quitar Marcas de Agua';
        processBtnIcon.textContent = 'auto_fix_high';
    });
});
