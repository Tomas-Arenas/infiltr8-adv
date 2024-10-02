<script>
    import { notifications, markNotificationAsOld, removeNotification } from '$lib/stores/notificationStore.js';
    import { Toast } from 'flowbite-svelte';
    import { fly, fade } from 'svelte/transition';
    import { BellRingSolid, CheckCircleSolid, ExclamationCircleSolid, InfoCircleSolid } from 'flowbite-svelte-icons';
  
    // Filter only new notifications
    let notificationMessages = $notifications.filter(notification => notification.new);
  
    function handleNotificationClose(id, type) {
        // Mark notification as no longer new
        markNotificationAsOld(id);
        // Remove temporary notifications from both store and backend
        removeNotification(id, type);
    }
  
    // Determine icon based on notification type
    function getIcon(type) {
        switch (type) {
            case 'success':
                return CheckCircleSolid;
            case 'error':
                return ExclamationCircleSolid;
            case 'alert':
                return ExclamationCircleSolid;
            case 'message':
                return InfoCircleSolid;
            case 'notification':
                return BellRingSolid;
            default:
                return BellRingSolid; // Default icon
        }
    }
  </script>
  
  <div class="fixed top-24 right-[10px] flex flex-col gap-1 z-[1050] max-h-[10px] min-w-[275px]">
    {#each notificationMessages as { id, message, type, timeout }}
        <div in:fade={{ duration: 800 }} out:fade={{ duration: 800 }} on:introend={() => setTimeout(() => handleNotificationClose(id, type), timeout)}>
            <Toast
                transition={fly}
                params={{ x: 200 }}
                color={type === 'success' ? 'green' : type === 'alert' ? 'red' : type === 'message' ? 'blue' : 'white'}  
                defaultIconClass='h-16 w-16'
                align={false}
                on:close={() => handleNotificationClose(id, type)}>
                <svelte:fragment slot="icon">
                    {#if type}
                        {#await getIcon(type) then Icon}
                            <Icon class="h-14 w-14" />
                        {/await}
                    {/if}
                </svelte:fragment>
                <div class="font-semibold text-base text-gray-900 dark:text-white">{titleCase(type)}</div>
                <div class="pt-1 text-base font-normal">{message}</div>
            </Toast>
        </div>
    {/each}
  </div>
  