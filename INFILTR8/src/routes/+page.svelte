<script>
	import { Heading, P, Button } from 'flowbite-svelte';
  	import { ArrowRightOutline } from 'flowbite-svelte-icons';
</script>

<div class="text-center">
  <Heading tag="h1" class="mb-4" customSize="text-4xl font-extrabold  md:text-5xl lg:text-6xl">WELCOME TO INFILTR8</Heading>
  <P class="mb-6 text-lg lg:text-xl sm:px-16 xl:px-48 dark:text-gray-400">Please go to login below.</P>
  <Button href="/login">
    Go to Login
    <ArrowRightOutline class="w-6 h-6 ms-2" />
  </Button>
</div>

<style>
	.container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		min-height: 100vh;
		text-align: center;
	}
	h1 {
		margin-bottom: 20px;
	}
	.button {
		background-color: #007bff;
		color: white;
		border: none;
		border-radius: 4px;
		padding: 10px 20px;
		font-size: 16px;
		cursor: pointer;
		text-decoration: none;
	}
	.button:hover {
		background-color: #0056b3;
	}
</style>
