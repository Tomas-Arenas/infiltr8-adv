<script>
    import { Input, Label, Helper, Button, Checkbox, A, ButtonGroup, InputAddon, ToolbarButton } from 'flowbite-svelte';
    import { EyeOutline, EyeSlashOutline } from 'flowbite-svelte-icons';
    let show = false;
    let show1 = false;


    let username=''
    let first_name = ''
    let last_name = ''
    let password = ''

    async function createUser() {
        const response = await fetch('/flask-api/create_user', {method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            first_name,
            last_name,
            username,
            password
        })
        });

        if (response.ok) {
        const result = await response.json();
        console.log(result);
        alert(result.status);
        } else {
        console.error('Failed to create user');
        alert('Failed to create user');
        }
    } 
  </script>
  
  <form id='createUserForm' on:submit|preventDefault={createUser} class='ml-72 mr-72'>
    <div class="grid gap-6 mb-6 md:grid-cols-2">
      <div>
        <Label for="first_name" class="mb-2">First name</Label>
        <Input bind:value={first_name} type="text" id="first_name" placeholder="John" required />
      </div>
      <div>
        <Label for="last_name" class="mb-2">Last name</Label>
        <Input bind:value={last_name} type="text" id="last_name" placeholder="Doe" required />
      </div>
    </div>
    <div class="mb-6">
      <Label for="username" class="mb-2">Username</Label>
      <Input bind:value={username} type="username" id="username" placeholder="JDoe21" required />
    </div>

    <div>
        <Label for="show-password" class="mb-2">Your password</Label>
        <Input bind:value={password} id="show-password" type={show ? 'text' : 'password'} placeholder="Your password here" size="lg">
            <button slot="left" on:click={() => (show = !show)} class="pointer-events-auto">
            {#if show}
                <EyeOutline class="w-6 h-6" />
            {:else}
                <EyeSlashOutline class="w-6 h-6" />
            {/if}
            </button>
        </Input>
        </div>

        <div>
        <Label for="show-password1" class="mb-2">Your password</Label>
        <ButtonGroup class="w-full">
            <InputAddon>
            <button on:click={() => (show1 = !show1)}>
                {#if show1}
                <EyeOutline class="w-6 h-6" />
                {:else}
                <EyeSlashOutline class="w-6 h-6" />
                {/if}
            </button>
            </InputAddon>
            <Input id="show-password1" type={show1 ? 'text' : 'password'} placeholder="Your password here" />
        </ButtonGroup>
        </div>

    <Button type="submit">Submit</Button>
  </form>